from PIL import Image
import os

if not os.path.exists('gif'):
    os.makedirs('gif')
os.system('rm -r tmp')
os.makedirs('tmp')

def gifify(png, path_prefix='png/', n_w=2, n_h=2):
    """
    Converts the png at the path within folder path_prefix, into small and large animated gifs.
    n_w and n_h specify the number of divisions to split the png into for the gifs (width-wise and
    height-wise)
    """
    im = Image.open(path_prefix + png)
    # we want to split it into n_w * n_h equal segments
    segments = []
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
    os.system('convert -delay 20 -dispose previous -loop 0 tmp/*_small.gif gif/%s_small.gif' % png.replace('.png', ''))
    os.system('rm tmp/*small.gif')
    # make big version
    os.system('convert -delay 20 -dispose previous -loop 0 tmp/*.gif gif/%s.gif' % png.replace('.png', ''))

    os.system('rm tmp/*png && rm tmp/*gif')

# make standard gifs
pngs = [f for f in os.listdir('png') if f.endswith('.png')]
print pngs
for png in pngs:
    gifify(png)

# make hard gifs
hard_pngs = [f for f in os.listdir('hard_png') if f.endswith('.png')]
print hard_pngs
for hard_png in hard_pngs:
    gifify(hard_png, path_prefix='hard_png/', n_w=3, n_h=3)


# cleanup
os.system('rm -r tmp')

