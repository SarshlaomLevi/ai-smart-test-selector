import argparse
from ai_smart_test_selector.pipeline.train import train_pipeline
from ai_smart_test_selector.pipeline.evaluate import evaluate_pipeline


def main(argv=None):
    parser = argparse.ArgumentParser(description="AI Smart Test Selector")

    parser.add_argument("--train", action="store_true")
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument("--run-all", action="store_true")

    args = parser.parse_args(argv)

    if args.train:
        train_pipeline()

    elif args.evaluate:
        model, X_test, y_test = train_pipeline()
        evaluate_pipeline(model, X_test, y_test)

    elif args.run_all:
        model, X_test, y_test = train_pipeline()
        evaluate_pipeline(model, X_test, y_test)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
