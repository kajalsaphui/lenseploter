from math import radians
from django.http.response import JsonResponse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse
import io
import base64


def plot_data(red_r,angle_r):
    angle_ref = angle_r
    lux_ref= red_r
    angle=angle_ref
    print("redious",red_r)
    print("angle",angle_ref)

    angle = [radians(a) for a in angle]

    lux=lux_ref

    # plt.clf()
    sp,(ax1, ax2) = plt.subplots(1, 2, subplot_kw=dict(projection='polar'))
    sp,ax1.set_theta_zero_location('E')
    sp,ax1.set_theta_direction(1)
    sp,ax2.set_theta_zero_location('W')
    sp,ax2.set_theta_direction(-1)
    ax1.plot(angle, lux)
    ax2.plot(angle, lux)
    ax1.set_yticklabels([])
    ax2.set_yticklabels([])
    ax1.set_xticklabels([])
    ax2.set_xticklabels([])
    ax1.grid(False)
    ax2.grid(False)
    ax1.spines['polar'].set_visible(False)
    ax2.spines['polar'].set_visible(False)
    plt.subplots_adjust(left=0.0,
                        bottom=0.0, 
                        right=0.9, 
                        top=0.9, 
                        wspace=0.0, 
                        hspace=0.0)
    # plt.show()
    f = io.BytesIO()
    sp.savefig(f, format="png", facecolor=(0.95, 0.95, 0.95))
    encoded_img = base64.b64encode(f.getvalue()).decode('utf-8').replace('\n', '')
    context = {"shape":encoded_img}
    # f.close()
    # return JsonResponse('<img src="data:image/png;base64,%s" />' % encoded_img, safe=False)
    # response = HttpResponse(content_type = 'image/png')
    # canvas = FigureCanvasAgg(sp)
    # canvas.print_png(response)
    return context