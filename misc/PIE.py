import numpy as np
from PIL import Image

def create_image_pyramid(image, mask, n_levels, gamma):
    masks = []
    images = []
    for i in range(n_levels):
        # Resample mask
        resampled_mask = mask[::2**i, ::2**i]
        masks.append(resampled_mask)
        
        # Resample and degamma image
        resampled_image = np.array(
            image.resize((resampled_mask.shape[1], resampled_mask.shape[0]), Image.BOX)
        ).astype(np.float64) / 255
        resampled_image_degammaed = np.power(resampled_image, 1/gamma)
        images.append(resampled_image_degammaed)

    return images, masks

def apply_laplacian_filter(a):
    return (
        a[1:-1, :-2] + a[1:-1, 2:] +
        a[2:, 1:-1] + a[:-2, 1:-1] -
        4 * a[1:-1, 1:-1]
    )

def do_poisson_edit_per_channel(dst, src, mask, n, err_threshold):
    dst_ = np.copy(dst)
    for i in range(n):
        dst_new = (
            apply_laplacian_filter(dst_) / 4
            + dst_[1:-1, 1:-1]
            - apply_laplacian_filter(src) / 4
        )
        max_err = np.max(
            np.abs(dst_[1:-1, 1:-1][mask[1:-1, 1:-1]]
            - dst_new[mask[1:-1, 1:-1]])
        )
        dst_new_padded = np.pad(dst_new, 1, mode="edge")
        dst_[mask] = dst_new_padded[mask]
        if max_err < err_threshold:
            break
    return dst_, max_err, i

def format_info(result, channel):
    return f"{channel} Error: {result[1]:.5f} Iter: {result[2]}"

def do_poisson_edit(dst, src, mask, n=10_000, err_threshold=1e-3):
    r_result = do_poisson_edit_per_channel(dst[:, :, 0], src[:, :, 0], mask, n, err_threshold)
    print(format_info(r_result, "R"), end=" ")
    g_result = do_poisson_edit_per_channel(dst[:, :, 1], src[:, :, 1], mask, n, err_threshold)
    print(format_info(g_result, "G"), end=" ")
    b_result = do_poisson_edit_per_channel(dst[:, :, 2], src[:, :, 2], mask, n, err_threshold)
    print(format_info(b_result, "B"))
    return np.dstack([r_result[0], g_result[0], b_result[0]])

def main():
    # Parameters
    max_iter = 10000  # 10000
    err_threshold = 1e-2  # 1e-2
    gamma = 2.2
    n_levels = 7

    # Load images and mask
    dst_image = Image.open("1721977717.484859.png")
    src_image = Image.open("a.png")
    mask = np.full((512, 512), 1)
    mask[:256, :] = 0

    # Initialize
    dst_images, masks = create_image_pyramid(dst_image, mask, n_levels, gamma)
    src_images, _ = create_image_pyramid(src_image, mask, n_levels, gamma)
    results = [None] * len(dst_images)

    # Compute
    for i in range(n_levels):
        level = n_levels - 1 - i
        s = src_images[level]
        d = np.copy(dst_images[level])
        m = masks[level]
        if i == 0:
            results[level] = do_poisson_edit(d, s, m, n=max_iter, err_threshold=err_threshold)
        else:
            # Upsample
            prev_result = results[level + 1]
            prev_d = np.stack([
                np.array(Image.fromarray(prev_result[:, :, ch]).resize((d.shape[1], d.shape[0]), Image.BILINEAR))
                for ch in range(3)
            ], axis=-1)
            d[m] = prev_d[m]
            results[level] = do_poisson_edit(d, s, m, n=max_iter, err_threshold=err_threshold)
        Image.fromarray((results[level] * 256).astype(np.uint8)).save(f"result_{level}.png")

if __name__ == '__main__':
    main()
