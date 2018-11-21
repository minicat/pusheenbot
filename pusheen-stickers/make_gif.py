from PIL import Image
import os

if not os.path.exists('gif'):
    os.makedirs('gif')
os.system('rm -r tmp')
os.makedirs('tmp')

def gifify(png, path_prefix='png/'):
    """
    Converts the png at the path within folder path_prefix, into small and large animated gifs.

    The number of divisions to split the ping into (n_w, n_h, width-wise and height-wise) is read
    out of the png name (ie image_w_h.png)
    """
    im = Image.open(path_prefix + png)
    path_components = png.rstrip('.png').split('_')
    n_w = int(path_components[-2])
    n_h = int(path_components[-1])
    final_name = '_'.join(path_components[:-2])

    # we want to split it into n_w * n_h equal segments
    w, h = im.size
    segment_w = w/n_w
    segment_h = h/n_h
    for i in range(n_h):
        for j in range(n_w):
            # left, upper, right, lower
            left =  segment_w*j
            upper = segment_h*i
            coords = (
                left,
                upper,
                left + segment_w,
                upper + segment_h,
            )
            segment = im.crop(coords)
            # segment.show()
            segment_name = '%d-%d' % (i, j)
            segment.save('tmp/' + segment_name + '.png')

            # filter out any empty frames
            greyscale_extrema = segment.convert("L").getextrema()
            if greyscale_extrema != (0, 0):
                # convert to gif, flattening to preserve smooth edges
                os.system('convert -flatten tmp/{0}.png tmp/{0}.gif'.format(segment_name))

                # resize down for small version
                os.system('convert tmp/{n}.gif -resize {w}x{h} -unsharp 0x0.75+0.75+0.008 tmp/{n}_small.gif'.format(
                    n=segment_name, w=segment_w//1.75, h=segment_h//1.75))

    # make small version
    os.system('convert -delay 20 -dispose previous -loop 0 tmp/*_small.gif gif/%s_small.gif' % final_name)
    os.system('rm tmp/*small.gif')
    # make big version
    os.system('convert -delay 20 -dispose previous -loop 0 tmp/*.gif gif/%s.gif' % final_name)

    os.system('rm tmp/*png && rm tmp/*gif')

# make pusheen gifs
pngs = [f for f in os.listdir('png') if f.endswith('.png')]
print pngs
for png in pngs:
    gifify(png)


# cleanup
os.system('rm -r tmp')

