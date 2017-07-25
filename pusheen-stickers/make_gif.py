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
            # os.system('convert tmp/{0}.png tmp/{0}.gif'.format(segment_name))
    os.system('convert -delay 20 -dispose previous -loop 0 tmp/*.png gif/%s.gif' % png.replace('.png', ''))
    os.system('rm tmp/*.png')



