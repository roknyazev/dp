import numpy as np
import vispy.app
from vispy import gloo
from vispy import visuals, scene
from vispy.visuals.transforms import STTransform, NullTransform


def get_image():
    """Load an image from the demo-data repository if possible. Otherwise,
    just return a randomly generated image.
    """
    from vispy.io import load_data_file, read_png

    try:
        return read_png(load_data_file('mona_lisa/mona_lisa_sm.png'))
    except Exception as exc:
        # fall back to random image
        print("Error loading demo image data: %r" % exc)

    # generate random image
    image = np.random.normal(size=(100, 100, 3))
    image[20:80, 20:80] += 3.
    image[50] += 3.
    image[:, 50] += 3.
    image = ((image - image.min()) *
             (253. / (image.max() - image.min()))).astype(np.ubyte)

    return image


def build_arrows(zpos=-1, color='white'):
    x1 = np.random.randint(50, 650, (200, 2))
    x2 = x1 + np.random.randint(-20, 20, (200, 2))
    x3 = np.zeros((x1.shape[0] * 2, 2))
    x3[::2] = x1
    x3[1::2] = x2
    x3 = x3[:, [0, 1, 1]]
    x3[:, 2] = zpos

    arrows = scene.visuals.Arrow(
        pos=x3,
        color=color,
        connect='segments',
        arrows=x3.reshape((-1, 6)),
        # method='gl',
        arrow_color=color,
        arrow_size=12,
        arrow_type='curved',
        antialias=True,
    )
    return arrows


canvas = scene.SceneCanvas(keys='interactive')
mona = get_image()
canvas.size = mona.shape[1], mona.shape[0]
canvas.show()

# Set up a viewbox to display the image with interactive pan/zoom
view = canvas.central_widget.add_view()
image = scene.visuals.Image(mona, interpolation='nearest', parent=view.scene, method='subdivide')

view.camera = scene.PanZoomCamera(aspect=1)
view.camera.flip = (0, 1, 0)  ## otherwise she's upside down.
view.camera.set_range()

# s = 700. / max(image.size)
# t = 0.5 * (700. - (image.size[0] * s)) + 50
# image.transform = STTransform(scale=(s, s), translate=(t, 50))

arr1 = build_arrows(-100, 'blue')
arr1.parent = image
arr2 = build_arrows(100, 'white')
arr2.parent = image

vispy.app.run()