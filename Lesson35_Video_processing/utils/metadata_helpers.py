"""Metadata formatting and display helpers. Author: Yair Levi"""

from pathlib import Path
from typing import Dict, List, Tuple
from datetime import timedelta
from ..config import get_resolution_name


def format_duration(seconds: float) -> str:
    """Format duration in seconds to HH:MM:SS.mmm format."""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:03d}"


def format_bitrate(bitrate: int) -> str:
    """Format bitrate in bps to human-readable format."""
    if bitrate >= 1_000_000:
        return f"{bitrate / 1_000_000:.2f} Mbps"
    elif bitrate >= 1_000:
        return f"{bitrate / 1_000:.2f} kbps"
    else:
        return f"{bitrate} bps"


def extract_stream_info(metadata: Dict) -> Tuple[Dict, Dict]:
    """Extract video and audio stream information from metadata."""
    video_info = None
    audio_info = None
    
    for stream in metadata.get('streams', []):
        if stream.get('codec_type') == 'video' and video_info is None:
            video_info = {
                'codec_name': stream.get('codec_name', 'Unknown'),
                'codec_long_name': stream.get('codec_long_name', 'Unknown'),
                'width': stream.get('width', 0),
                'height': stream.get('height', 0),
                'pix_fmt': stream.get('pix_fmt', 'Unknown'),
                'fps': eval(stream.get('r_frame_rate', '0/1')),
                'bit_rate': int(stream.get('bit_rate', 0))
            }
        elif stream.get('codec_type') == 'audio' and audio_info is None:
            audio_info = {
                'codec_name': stream.get('codec_name', 'Unknown'),
                'sample_rate': int(stream.get('sample_rate', 0)),
                'channels': stream.get('channels', 0),
                'channel_layout': stream.get('channel_layout', 'Unknown'),
                'bit_rate': int(stream.get('bit_rate', 0))
            }
    
    return video_info, audio_info


def print_metadata_report(video_path: Path, metadata: Dict, gop_stats: Dict, frames: List[Dict]) -> None:
    """Print formatted metadata report to console."""
    print("\n" + "=" * 70)
    print("VIDEO METADATA ANALYSIS REPORT")
    print("=" * 70)
    
    format_info = metadata.get('format', {})
    print(f"\nFile: {video_path.name}")
    print(f"Full Path: {video_path}")
    print(f"Container Format: {format_info.get('format_long_name', 'Unknown')}")
    
    duration = float(format_info.get('duration', 0))
    print(f"Duration: {format_duration(duration)} ({duration:.3f} seconds)")
    
    video_info, audio_info = extract_stream_info(metadata)
    
    if video_info:
        print(f"\n{'VIDEO STREAM':^70}")
        print("-" * 70)
        print(f"Codec: {video_info['codec_name']} ({video_info['codec_long_name']})")
        resolution_name = get_resolution_name(video_info['width'], video_info['height'])
        print(f"Resolution: {video_info['width']}x{video_info['height']} ({resolution_name})")
        print(f"Pixel Format: {video_info['pix_fmt']}")
        print(f"Frame Rate: {video_info['fps']:.2f} fps")
        if video_info['bit_rate'] > 0:
            print(f"Bitrate: {format_bitrate(video_info['bit_rate'])}")
    
    if audio_info:
        print(f"\n{'AUDIO STREAM':^70}")
        print("-" * 70)
        print(f"Codec: {audio_info['codec_name']}")
        print(f"Sample Rate: {audio_info['sample_rate']} Hz")
        print(f"Channels: {audio_info['channels']} ({audio_info['channel_layout']})")
        if audio_info['bit_rate'] > 0:
            print(f"Bitrate: {format_bitrate(audio_info['bit_rate'])}")
    
    _print_gop_and_frames(gop_stats, frames)


def _print_gop_and_frames(gop_stats: Dict, frames: List[Dict]) -> None:
    """Print GOP analysis and frame samples."""
    print(f"\n{'GOP STRUCTURE ANALYSIS':^70}")
    print("-" * 70)
    print(f"Total Frames: {gop_stats['total_frames']}")
    print(f"I-Frames: {gop_stats['i_frames']} ({gop_stats['i_percentage']:.1f}%)")
    print(f"P-Frames: {gop_stats['p_frames']} ({gop_stats['p_percentage']:.1f}%)")
    print(f"B-Frames: {gop_stats['b_frames']} ({gop_stats['b_percentage']:.1f}%)")
    print(f"Total GOPs: {gop_stats['gop_count']}")
    print(f"Average GOP Size: {gop_stats['avg_gop_size']:.1f} frames")
    
    print(f"\n{'FRAME SAMPLES':^70}")
    print("-" * 70)
    print(f"{'Frame #':<10} {'Timestamp (s)':<15} {'Type':<10}")
    print("-" * 70)
    
    for i, frame in enumerate(frames[:10]):
        pts_time = float(frame.get('pts_time', 0))
        pict_type = frame.get('pict_type', '?')
        print(f"{i:<10} {pts_time:<15.3f} {pict_type:<10}")
    
    if len(frames) > 20:
        print("...")
        for i, frame in enumerate(frames[-10:], start=len(frames) - 10):
            pts_time = float(frame.get('pts_time', 0))
            pict_type = frame.get('pict_type', '?')
            print(f"{i:<10} {pts_time:<15.3f} {pict_type:<10}")
    
    print("=" * 70 + "\n")
