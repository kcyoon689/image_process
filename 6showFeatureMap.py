import numpy as np
from matplotlib import pyplot

featureMaps = np.load('feature_map.npy')
print(len(featureMaps))
print(len(featureMaps[0]))
print(len(featureMaps[0][0]))

featureMaps_np = np.asarray(featureMaps)
print(featureMaps_np.shape)

square = 16
for idx in range(square):
  for jdx in range(square):
    pyplot.subplot(square, square, idx * square + jdx + 1)
    pyplot.imshow(featureMaps[:,:,idx * square + jdx], cmap='gray')
pyplot.show()
pyplot.savefig('feature_map.png', dpi=1000)




# demo/demo_image.py

# np.save('/home/crvl-yoon/mmdetection/demo/feature_map.npy', x_np)
# # featureMaps = np.load('/home/crvl-yoon/mmdetection/demo/feature_map.npy')
# # featureMaps_np = np.asarray(featureMaps)

# featureMaps_np = x_np

# os.makedirs('/home/crvl-yoon/mmdetection/demo/feature_map', exist_ok=True)
# head, tail = os.path.split(args.img)

# images = 4
# square = 8
# for kdx in range(images):
#     for idx in range(square):
#         for jdx in range(square):
#             pyplot.subplot(square, square, idx * square + jdx + 1)
#             pyplot.imshow(featureMaps_np[:,:,idx * square + jdx], cmap='gray')
#     # pyplot.savefig('/home/crvl-yoon/mmdetection/demo/feature_map_' + str(kdx) + '.png', dpi=1000)
#     pyplot.savefig('/home/crvl-yoon/mmdetection/demo/feature_map/' + tail.split('.')[0] + '_' + str(kdx) + '.png', dpi=1000)
#     # pyplot.show()

# img_input = cv2.imread(args.img)
# cv2.imwrite('/home/crvl-yoon/mmdetection/demo/feature_map/' + tail, img_input)
# # show_result_pyplot(
# #     model,
# #     args.img,
# #     result,
# #     palette=args.palette,
# #     score_thr=args.score_thr)
