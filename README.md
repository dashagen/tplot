## Introduction
**tplot** is a perl script for minimalistic terminal plotting which is primarily designed for line plots for not more than 3 series. After all it's terminal plotting, any sophisticated plotting options will not fare well even if equipped. 

## Usage
```bash
NAME
    tplot - A simple terminal plotting tool

SYNOPSIS
    tplot -r col1[,col2,..] [-b col] [-s hieght,width] [-y min,max] [-f
    format] [-l legend1, legend2, ..] [-h] [file]

OPTIONS
    The following options are supported:

    -r col1[,col2,..]
                List the column numbers that are to be included in the plot.

    -b col      Column to be used for labels.

    -s height,width
                The size of the plotting area. Default height is 15 and
                default width is 100.

    -y min,max  Set min and max of the y axis.

    -f format   Format of the y-axis label. If not selected, it will be
                decided based on the max absolute value of the input. "m"
                for millions. "p" for percentage. "k" for thousands.

    -l legend1, legend2,...
                Legends for each series. If not selected, numbers will be
                used.

    -h          Print this help message.

```

## Examples
```bash
% cat doc/test_dat2.txt |awk '{print $1, ($5+2)/100, ($5+$2/0.8+2)/100}' | ./tplot -r2,3 -l "mean,observed" -y0 -fp -b1
```
<img src="./doc/ex1.png" width="850"/>

