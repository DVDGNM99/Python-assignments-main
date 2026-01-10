import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List
from datetime import timedelta
import logging

from .models import ReportStats

logger = logging.getLogger(__name__)

def generate_plots(stats: ReportStats, out_dir: Path):
    """
    Generates a boxplot of deltas (hours) per assignment.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Prepare data
    data = []
    labels = []
    
    # Sort by assignment name for consistent order
    sorted_items = sorted(stats.deltas_by_assignment.items())
    
    for assign, deltas in sorted_items:
        if not deltas:
            continue
        
        # Convert deltas to hours
        hours = [d.total_seconds() / 3600 for d in deltas]
        data.append(hours)
        labels.append(assign)
        
    if not data:
        logger.warning("No data for plotting.")
        return

    # Create Boxplot
    plt.figure(figsize=(12, 6))
    plt.boxplot(data, tick_labels=labels, showfliers=True) # showfliers=True to see outliers
    plt.title("Submission Deltas per Assignment (Hours)")
    plt.xlabel("Assignment")
    plt.ylabel("Delta (Hours) - Positive = Late")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add a horizontal line at 0 (Deadline)
    plt.axhline(0, color='r', linestyle='-', linewidth=1, label="Deadline")
    plt.legend()
    
    plt.tight_layout()
    
    out_path = out_dir / "deltas_boxplot.png"
    plt.savefig(out_path)
    plt.close()
    logger.info(f"Saved boxplot to {out_path}")

    # Optional: Violin Plot
    plt.figure(figsize=(12, 6))
    plt.violinplot(data, showmeans=True, showmedians=True)
    # Violin plot labels are harder, set ticks manually
    plt.xticks(range(1, len(labels) + 1), labels, rotation=45, ha='right')
    plt.title("Submission Deltas Distribution (Violin Plot)")
    plt.xlabel("Assignment")
    plt.ylabel("Delta (Hours)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.axhline(0, color='r', linestyle='-', linewidth=1)
    
    out_path_violin = out_dir / "deltas_violin.png"
    plt.savefig(out_path_violin)
    plt.close()
    logger.info(f"Saved violin plot to {out_path_violin}")
