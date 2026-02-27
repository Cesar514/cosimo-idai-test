import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import hashlib
from datetime import datetime

# Style Tokens from STYLE_PLAN.md
COLORS = {
    'bg_canvas': '#F4F7FB',
    'bg_card': '#FFFFFF',
    'text_primary': '#0F172A',
    'text_secondary': '#475569',
    'accent_primary': '#0B5FFF',
    'accent_secondary': '#00A3A3',
    'accent_warm': '#FF7A18',
    'status_success': '#0E9F6E',
    'line_default': '#D1D9E6'
}

# Mapping of planners to human-readable labels used in the paper figures
PLANNER_LABELS = {
    'astar': 'A*',
    'dijkstra': 'Dij',
    'greedy_best_first': 'GBF',
    'r1_weighted_astar': 'R1',
    'r2_bidirectional_astar': 'R2',
    'r3_theta_star': 'R3',
    'r4_idastar': 'R4',
    'r5_jump_point_search': 'R5',
    'r6_lpa_star': 'R6',
    'r7_beam_search': 'R7',
    'r8_fringe_search': 'R8',
    'r9_bidirectional_bfs': 'R9'
}

def setup_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'figure.facecolor': COLORS['bg_canvas'],
        'axes.facecolor': COLORS['bg_card'],
        'text.color': COLORS['text_primary'],
        'axes.labelcolor': COLORS['text_primary'],
        'xtick.color': COLORS['text_secondary'],
        'ytick.color': COLORS['text_secondary'],
        'grid.color': COLORS['line_default'],
        'font.family': 'sans-serif',
        'font.sans-serif': ['IBM Plex Sans', 'DejaVu Sans', 'Arial', 'Helvetica'],
        'axes.titlesize': 16,
        'axes.labelsize': 14,
        'legend.fontsize': 12,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12
    })

def get_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_plots(csv_path, output_dir):
    df = pd.read_csv(csv_path)
    df['planner_label'] = df['planner'].map(PLANNER_LABELS)

    # Sort planners by mean solve time for consistency
    order = df.groupby('planner_label')['solve_time_ms'].mean().sort_values().index

    os.makedirs(output_dir, exist_ok=True)

    # 1. Mean Solve Time
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df, x='planner_label', y='solve_time_ms', order=order, color=COLORS['accent_primary'])
    plt.yscale('log')
    plt.title(f'Mean Planner Solve Time on {df["maze_index"].nunique()} Mazes')
    plt.xlabel('Planner')
    plt.ylabel('Mean solve time (ms) (log10 scale)')

    # Add values on top of bars
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha = 'center', va = 'center',
                    xytext = (0, 9),
                    textcoords = 'offset points')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'benchmark_runtime_ms.png'), dpi=300)
    plt.savefig(os.path.join(output_dir, 'benchmark_runtime_ms.pdf'))
    plt.close()

    # 2. Mean Expansions
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df, x='planner_label', y='expansions', order=order, color=COLORS['accent_secondary'])
    plt.yscale('log')
    plt.title('Mean Node Expansions')
    plt.xlabel('Planner')
    plt.ylabel('Mean Expansions (log10 scale)')

    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha = 'center', va = 'center',
                    xytext = (0, 9),
                    textcoords = 'offset points')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'benchmark_expansions.png'), dpi=300)
    plt.savefig(os.path.join(output_dir, 'benchmark_expansions.pdf'))
    plt.close()

    # 3. Success Rate
    plt.figure(figsize=(10, 6))
    success_df = df.groupby('planner_label')['success'].mean().reset_index()
    ax = sns.barplot(data=success_df, x='planner_label', y='success', order=order, color=COLORS['status_success'] if 'status_success' in COLORS else COLORS['accent_secondary'])
    plt.title('Success Rate')
    plt.xlabel('Planner')
    plt.ylabel('Success Rate (0.0 - 1.0)')
    plt.ylim(0, 1.1)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'benchmark_success_rate.png'), dpi=300)
    plt.savefig(os.path.join(output_dir, 'benchmark_success_rate.pdf'))
    plt.close()

    # 4. Runtime Uncertainty (Boxplot)
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='planner_label', y='solve_time_ms', order=order, hue='planner_label', palette="Blues", legend=False)
    plt.yscale('log')
    plt.title('Runtime Distribution and Uncertainty')
    plt.xlabel('Planner')
    plt.ylabel('Solve Time (ms) (log10 scale)')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'runtime_uncertainty.png'), dpi=300)
    plt.savefig(os.path.join(output_dir, 'runtime_uncertainty.pdf'))
    plt.close()

def update_manifest(csv_path, script_path, manifest_path):
    csv_hash = get_file_hash(csv_path)
    timestamp = datetime.now().isoformat()
    command = f"python {script_path}"

    header = "timestamp,script,artifact_hash,command\n"
    new_entry = f"{timestamp},{script_path},{csv_hash},{command}\n"

    if not os.path.exists(manifest_path):
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        with open(manifest_path, 'w') as f:
            f.write(header)

    with open(manifest_path, 'a') as f:
        f.write(new_entry)

if __name__ == "__main__":
    CSV_INPUT = 'robotics_maze/results/benchmark_results.csv'
    OUTPUT_DIR = 'paper/ieee_tro_robotics_maze/figures'
    MANIFEST = 'robotics_maze/coordination/figure_manifest.csv'
    SCRIPT = 'robotics_maze/scripts/generate_publication_plots.py'

    setup_style()
    generate_plots(CSV_INPUT, OUTPUT_DIR)
    update_manifest(CSV_INPUT, SCRIPT, MANIFEST)
    print(f"Figures generated in {OUTPUT_DIR}")
    print(f"Manifest updated: {MANIFEST}")
