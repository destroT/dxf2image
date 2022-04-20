import matplotlib.pyplot as plt
from ezdxf import recover
from ezdxf import DXFStructureError
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend


def dxf2image(dxffile, destination_name):
    try:
        doc, auditor = recover.readfile(dxffile)
    except IOError as e:
        raise IOError("Not a DXF file or a generic I/O error.") from e
    except DXFStructureError as e:
        raise DXFStructureError("Invalid or corrupted DXF file.") from e
    # The auditor.errors attribute stores severe errors,
    # which may raise exceptions when rendering.
    if not auditor.has_errors:
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(doc)
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(doc.modelspace(), finalize=True)
        fig.savefig(destination_name, dpi=300)


if __name__ == "__main__":
    dxf2image("raster.dxf", "raster.jpg")
