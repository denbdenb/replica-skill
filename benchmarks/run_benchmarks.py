import os
import sys
import time
import tracemalloc
import tempfile
import shutil

# Add paths to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS_DIR = os.path.join(BASE_DIR, ".agents", "skills")

sys.path.insert(0, os.path.join(AGENTS_DIR, "replica-brand"))
sys.path.insert(0, os.path.join(AGENTS_DIR, "replica-design"))
sys.path.insert(0, os.path.join(AGENTS_DIR, "replica-diff"))
sys.path.insert(0, os.path.join(AGENTS_DIR, "replica-entrepreneur"))
sys.path.insert(0, os.path.join(AGENTS_DIR, "replica-launch"))

import contrast
import reviews
import sweep
import imgdiff

def benchmark_contrast():
    # Test luminance and ratio on 1000 pairs
    colors = ["#ffffff", "#000000", "#123456", "#abcdef", "#6b7280", "#3b82f6", "#ef4444", "#10b981"]
    tracemalloc.start()
    t0 = time.perf_counter()
    for _ in range(500):
        for c1 in colors:
            for c2 in colors:
                r = contrast.ratio(c1, c2)
    t1 = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"elapsed_ms": (t1 - t0) * 1000, "peak_kb": peak / 1024}

def benchmark_reviews():
    # Benchmark date parsing on 5,000 date strings of various formats
    test_dates = [
        "2024-03-15",
        "2023-11",
        "2024-02-29",
        "2024-01-01 12:00:00",
        "invalid-date",
        "",
        "2022-12-31T23:59:59Z",
        " 2023-05-20 "
    ] * 625  # 5,000 total
    tracemalloc.start()
    t0 = time.perf_counter()
    for d in test_dates:
        reviews.parse_date(d)
    t1 = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"elapsed_ms": (t1 - t0) * 1000, "peak_kb": peak / 1024}

def benchmark_sweep():
    # Create a synthetic repo of 100 files, each 500 lines
    temp_dir = tempfile.mkdtemp(prefix="sweep_bench_")
    try:
        avoid = ["OriginalApp", "AcmeCorp", "LegacyBrand"]
        domains = ["originalapp.com", "acmecorp.io"]
        colors = ["#006bff", "#0ae8f0"]
        
        # Write files
        for i in range(100):
            fn = os.path.join(temp_dir, f"source_{i}.js")
            with open(fn, "w", encoding="utf-8") as f:
                for line_idx in range(500):
                    if line_idx % 50 == 0:
                        f.write(f"// Reference to AcmeCorp button here\n")
                    elif line_idx % 70 == 0:
                        f.write(f"const link = 'https://originalapp.com/login';\n")
                    elif line_idx % 90 == 0:
                        f.write(f"const brandColor = '#006bff';\n")
                    else:
                        f.write(f"function doSomething_{line_idx}() {{ return {line_idx} * 2; }}\n")
        
        tracemalloc.start()
        t0 = time.perf_counter()
        hits = sweep.sweep(temp_dir, avoid=avoid, domains=domains, colors=colors)
        t1 = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return {"elapsed_ms": (t1 - t0) * 1000, "peak_kb": peak / 1024, "hits": len(hits)}
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def benchmark_imgdiff():
    # Benchmark layout mode on generated PNGs
    width = 480
    height = 800
    rows1 = [[(255, 255, 255) for _ in range(width)] for _ in range(height)]
    rows2 = [[(255, 255, 255) for _ in range(width)] for _ in range(height)]
    
    # Put header and buttons
    for y in range(0, 80):
        for x in range(width):
            rows1[y][x] = (30, 30, 80)
            rows2[y][x] = (30, 30, 80)
    for y in range(120, 300):
        for x in range(40, 440):
            rows1[y][x] = (50, 50, 50)
            rows2[y][x] = (50, 50, 50)
    for y in range(400, 480):
        for x in range(40, 200):
            rows1[y][x] = (0, 100, 255)
    for y in range(450, 530):
        for x in range(40, 200):
            rows2[y][x] = (0, 100, 255)

    img1_path = os.path.join(tempfile.gettempdir(), "bench_img1.png")
    img2_path = os.path.join(tempfile.gettempdir(), "bench_img2.png")
    try:
        imgdiff.write_png(img1_path, width, height, rows1)
        imgdiff.write_png(img2_path, width, height, rows2)
        
        tracemalloc.start()
        t0 = time.perf_counter()
        img_a = imgdiff.read_png(img1_path)
        img_b = imgdiff.read_png(img2_path)
        res, diff = imgdiff.compare(img_a, img_b, mode="layout")
        t1 = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return {"elapsed_ms": (t1 - t0) * 1000, "peak_kb": peak / 1024, "score": res["score"]}
    finally:
        if os.path.exists(img1_path): os.remove(img1_path)
        if os.path.exists(img2_path): os.remove(img2_path)

if __name__ == "__main__":
    print("Running Baseline Benchmarks (5 repetitions each)...")
    
    # 1. contrast
    c_times = []
    c_peaks = []
    for _ in range(5):
        r = benchmark_contrast()
        c_times.append(r["elapsed_ms"])
        c_peaks.append(r["peak_kb"])
    print(f"contrast.py:  avg {sum(c_times)/5:.2f} ms, peak {max(c_peaks):.1f} KB")
    
    # 2. reviews
    rev_times = []
    rev_peaks = []
    for _ in range(5):
        r = benchmark_reviews()
        rev_times.append(r["elapsed_ms"])
        rev_peaks.append(r["peak_kb"])
    print(f"reviews.py:   avg {sum(rev_times)/5:.2f} ms, peak {max(rev_peaks):.1f} KB")
    
    # 3. sweep
    sw_times = []
    sw_peaks = []
    hits = 0
    for _ in range(5):
        r = benchmark_sweep()
        sw_times.append(r["elapsed_ms"])
        sw_peaks.append(r["peak_kb"])
        hits = r["hits"]
    print(f"sweep.py:     avg {sum(sw_times)/5:.2f} ms, peak {max(sw_peaks):.1f} KB (hits: {hits})")
    
    # 4. imgdiff
    im_times = []
    im_peaks = []
    score = 0
    for _ in range(5):
        r = benchmark_imgdiff()
        im_times.append(r["elapsed_ms"])
        im_peaks.append(r["peak_kb"])
        score = r["score"]
    print(f"imgdiff.py:   avg {sum(im_times)/5:.2f} ms, peak {max(im_peaks):.1f} KB (score: {score})")
