import argparse
from ai_smart_test_selector.pipeline.train import train_pipeline
from ai_smart_test_selector.pipeline.evaluate import evaluate_pipeline


def main():
    parser = argparse.ArgumentParser(description="AI Smart Test Selector")

    parser.add_argument("--train", action="store_true")
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument("--run-all", action="store_true")

    args = parser.parse_args()

    if args.train:
        train_pipeline()

    elif args.evaluate:
        evaluate_pipeline()

    elif args.run_all:
        train_pipeline()
        evaluate_pipeline()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
