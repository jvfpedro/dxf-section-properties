# DXF Section Properties (Rasterization Method)

This repository contains a Python tool developed to calculate the geometric properties of complex cross-sections imported from DXF files.

Unlike traditional analytical methods that rely on formula decomposition, this script utilizes a **discretization approach (rasterization)**. It converts vector CAD drawings into high-resolution binary images and performs numerical integration over the pixels to determine properties like Area, Moment of Inertia, and Centroids.

## Features
- **DXF Parsing:** reads `.dxf` files using `ezdxf` to extract geometry (Lines, Polylines).
- **Rasterization:** converts vector geometry into a binary TIFF image, effectively discretizing the cross-section into a pixel grid.
- **Geometric Calculation:** algorithms to calculate:
  - Cross-sectional Area ($A$).
  - Centroid coordinates ($X_{CG}, Y_{CG}$).
  - Moments of Inertia ($I_x, I_y$) using the parallel axis theorem on a pixel level.
  - Section Moduli ($W_{inf}, W_{sup}$) and Kern limits ($k$).
- **Batch Processing:** capable of processing multiple sections and depths in sequence.

## Technologies Used
- **Python 3**
- **Ezdxf:** for reading and parsing CAD files.
- **Pillow (PIL):** for image creation and manipulation.
- **Numpy:** for efficient array operations and matrix calculations.
- **Rasterio:** for handling geospatial raster data (TIFF generation).

## Methodology
The script works in two main stages:
1.  **Image Generation:** the DXF geometry is mapped to a high-resolution pixel grid. The resolution (`res`) defines the accuracy of the discretization.
2.  **Pixel Integration:** the code iterates through the generated matrix. Each pixel is treated as a differential area element ($dA$). The properties are calculated by summing the contribution of each active pixel relative to the axes.

## Installation and Setup
1.  Install Python 3.
2.  Install the required dependencies:
    ```bash
    pip install ezdxf numpy pillow rasterio
    ```
3.  Clone this repository.

## How to Use
1.  Organize your files:
    - Place your CAD files in a folder named `dxf/`.
    - Create a folder named `tif/` for the output images.
2.  Open `dxf_2_tif.py`.
3.  Configure the input file paths and the section depth (`D`) at the end of the script:
    ```python
    # Example usage inside the script
    img = dxf_para_tiff("dxf/section_01.dxf", res=0.1, output_tif="tif/output_01.tif")
    calc.processa(img, D=2100)
    ```
4.  Run the script. The geometric properties will be printed in the console.

## Notes
- **Resolution:** the accuracy of the calculation depends on the resolution (`res`) set during the rasterization process. Smaller values yield higher precision but increase processing time.
- **Use Case:** this method is particularly useful for arbitrary or organic shapes where standard analytical formulas are difficult to apply.

## Author
João Vitor Ferreira Pedro Engineering Student GitHub: https://github.com/jvfpedro

Daniel Tavares dos Anjos Engineering Student at UFSC GitHub: https://github.com/danieltanjos
