import marimo

__generated_with = "0.19.9"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ///admonition | Usage
    - Define a width for the source image, and a width for the browser display.
    - Click on the image to see relative and absolute pixel values.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Use HTML canvas to get image coordinates
    """)
    return


@app.cell(hide_code=True)
def _(mo, srcw, w):
    mo.md(f"*Width of image to import* {srcw} *Width of display*: {w}")

    return


@app.cell(hide_code=True)
def _(canvas, mo):
    click = canvas.click
    msg = ""

    if isinstance(click, dict) and "x" in click and "y" in click:
        disp_w = click.get("displayWidth")
        disp_h = click.get("displayHeight")
        nat_w = click.get("naturalWidth")
        nat_h = click.get("naturalHeight")
        if all(isinstance(v, int) and v > 0 for v in [disp_w, disp_h, nat_w, nat_h]):
            x_disp = int(click["x"])
            y_disp = int(click["y"])
            x_px = int(round(x_disp * nat_w / disp_w))
            y_px = int(round(y_disp * nat_h / disp_h))
            x_norm = min(max(x_px / nat_w, 0.0), 1.0)
            y_norm = min(max(y_px / nat_h, 0.0), 1.0)

            msg = (
                """
    **Source image**            
    Width, height: {nat_w}x{nat_h}            
    **Coordinates of clicked point**  
    Displayed pixels: x={x_disp}, y={y_disp}  
    Original pixels: x={x_px}, y={y_px}  
    Normalized: x={x_norm:.4f}, y={y_norm:.4f}  



    """.format(
                    x_disp=x_disp,
                    y_disp=y_disp,
                    x_px=x_px,
                    y_px=y_px,
                    x_norm=x_norm,
                    y_norm=y_norm,
                    nat_w=nat_w,
                    nat_h=nat_h,

                )
            )

    mo.md(msg)
    return (click,)


@app.cell(hide_code=True)
def _(canvas):
    canvas
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html("<hr/><hr/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Computation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **UI**
    """)
    return


@app.cell
def _(mo):
    srcw = mo.ui.slider(start=600, stop=4000, step=100, show_value=True, value=1000)
    return (srcw,)


@app.cell
def _(mo):
    w = mo.ui.slider(start=100, stop=900, step=25, show_value=True, value=500)
    return (w,)


@app.cell
def _(CanvasClick, data_url, mo, w):
    canvas = mo.ui.anywidget(CanvasClick(src=data_url, width=w.value))
    return (canvas,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Image** (with source width defined by user interaction)
    """)
    return


@app.cell
def _(srcw):
    url = f"https://www.homermultitext.org/iipsrv?OBJ=IIP,1.0&FIF=/project/homer/pyramidal/deepzoom/citebne/complutensian/v1/v1p19.tif&RGN=0.007111,0.0006196,0.9880,0.9991&WID={srcw.value}&CVT=JPEG"
    return (url,)


@app.cell
def _(base64, requests, url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    encoded = base64.b64encode(response.content).decode("ascii")
    data_url = f"data:image/jpeg;base64,{encoded}"
    return (data_url,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Canvas widget**
    """)
    return


@app.cell
def _(anywidget, traitlets):
    class CanvasClick(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
          const container = document.createElement("div");
          const canvas = document.createElement("canvas");
          canvas.style.cursor = "crosshair";
          container.appendChild(canvas);
          el.appendChild(container);

          let img = new Image();
          img.crossOrigin = "anonymous";

          const draw = () => {
            const width = model.get("width");
            if (!img.complete || img.naturalWidth === 0) return;
            const scale = width / img.naturalWidth;
            const height = Math.round(img.naturalHeight * scale);
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext("2d");
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
          };

          const setSrc = () => {
            const src = model.get("src");
            img = new Image();
            img.crossOrigin = "anonymous";
            img.onload = () => {
              draw();
              model.set("image_info", {
                naturalWidth: img.naturalWidth,
                naturalHeight: img.naturalHeight,
              });
              model.save_changes();
            };
            img.src = src;
          };

          setSrc();
          model.on("change:src", setSrc);
          model.on("change:width", draw);

          canvas.addEventListener("click", (evt) => {
            const rect = canvas.getBoundingClientRect();
            const x = Math.round(evt.clientX - rect.left);
            const y = Math.round(evt.clientY - rect.top);
                        const dispW = canvas.width;
                        const dispH = canvas.height;
                        const natW = img.naturalWidth;
                        const natH = img.naturalHeight;
                        const xPx = Math.round(x * natW / dispW);
                        const yPx = Math.round(y * natH / dispH);
                        const xNorm = natW > 0 ? Math.min(Math.max(xPx / natW, 0), 1) : 0;
                        const yNorm = natH > 0 ? Math.min(Math.max(yPx / natH, 0), 1) : 0;
            model.set("click", {
              x,
              y,
                            displayWidth: dispW,
                            displayHeight: dispH,
                            naturalWidth: natW,
                            naturalHeight: natH,
                            xNorm,
                            yNorm,
            });
            model.save_changes();
          });
        }
        export default { render };
        """

        src = traitlets.Unicode("").tag(sync=True)
        width = traitlets.Int(500).tag(sync=True)
        click = traitlets.Dict({}).tag(sync=True)
        image_info = traitlets.Dict({}).tag(sync=True)

    return (CanvasClick,)


@app.cell
def _(click):
    click.keys()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Imports**
    """)
    return


@app.cell
def _():
    import anywidget
    import base64
    import requests
    import traitlets

    return anywidget, base64, requests, traitlets


if __name__ == "__main__":
    app.run()
