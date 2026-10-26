"""Build the eleven checked-in course pages from the shared renderer and data."""
from pathlib import Path
import argparse
from course import render
parser=argparse.ArgumentParser()
parser.add_argument('--output-root',type=Path,default=Path(__file__).resolve().parents[2])
args=parser.parse_args()
for number in range(1,12):print(render(number,args.output_root))
