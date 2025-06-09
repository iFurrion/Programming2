import random
import matplotlib.pyplot as plt

random.seed(40)

def collect_data(func):
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        return data
    return wrapper

@collect_data
def roll_10():
    return [random.randint(1, 6) for _ in range(10)]

@collect_data
def roll_100():
    return [random.randint(1, 6) for _ in range(100)]

@collect_data
def roll_1000():
    return [random.randint(1, 6) for _ in range(1000)]

@collect_data
def roll_10000():
    return [random.randint(1, 6) for _ in range(10000)]

@collect_data
def roll_500000():
    return [random.randint(1, 6) for _ in range(500000)]

if __name__ == "__main__":
    roll_funcs = [roll_10, roll_100, roll_1000, roll_10000, roll_500000]
    titles = ["10", "100", "1000", "10000", "500000"]

    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(16, 8))
    axs = axs.flatten()

    for i, (func, title) in enumerate(zip(roll_funcs, titles)):
        data = func()
        axs[i].hist(data, bins=range(1, 8), align='left', rwidth=0.8, edgecolor='black')
        axs[i].set_title(f"{title} Rolls", fontsize=12)
        axs[i].set_xticks(range(1, 7))
        axs[i].set_xlabel("Value")
        axs[i].set_ylabel("Frequency")
        axs[i].grid(True, linestyle='--', alpha=0.5)

   
    fig.delaxes(axs[-1])

    plt.tight_layout(pad=3.0)
    plt.show()


