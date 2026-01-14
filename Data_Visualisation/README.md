# HDV-Lib14 Nucleotide Heatmap Visualizer

An interactive Python tool for visualizing nucleotide sequences and fitness data from HDV-Lib14 experiments.

![Nucleotide Colormap Visualization](https://github.com/vincbeaulieu/HDV-LIG14/blob/main/Data_Visualisation/nt_colormap.png)

## Features

- **Interactive nucleotide heatmap** with customizable color schemes
- **Dual fitness visualizations** with log-scale colorbars
- **Real-time color customization** with 12-color palette selector
- **Data refresh functionality** for live Excel file updates
- **Position-based labeling** using column headers

## Requirements
```bash
pip install openpyxl numpy matplotlib
```

## Usage

1. Have your Excel file at `Data_Visualisation/HDV-Lib14.xlsx`
2. Ensure your data structure:
   - Columns G-T: Individual nucleotide positions
   - Column B: Fitness metric 1
   - Column D: Fitness metric 2
3. Run the script as a module from project root:
```bash
python -m Data_Visualisation.nucleotide_visualizer
```

## Controls

- **Color selector buttons**: Click to change nucleotide colors (A, T, C, G)
- **Reset Colors**: Restore default color scheme
- **Refresh Data**: Reload data from Excel file

## Data Format

The tool expects an Excel file with:
- Row 1: Skipped
- Row 2: Headers (including position labels in columns G-T)
- Row 3+: Data rows with nucleotides in columns G-T and fitness values in columns B and D

## License

MIT License
