from PIL import Image
import os

pngs = [f for f in os.listdir('png') if f.endswith('.png')]
print pngs

if not os.path.exists('gif'):
    os.makedirs('gif')
os.system('rm -r tmp')
os.makedirs('tmp')

for png in pngs:
    im = Image.open('png/'+png)
    # we want to split it into 4 equal segments
    segments = []
    w, h = im.size
    n_w = 2
    n_h = 2
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



