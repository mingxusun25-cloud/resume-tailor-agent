from __future__ import annotations

import argparse
from pathlib import Path

from resumetailor_agent.config import AppConfig
from resumetailor_agent.evaluator import evaluate_cases_file
from resumetailor_agent.workflow import run_resume_tailor, run_resume_tailor_compare


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run ResumeTailor Agent from the command line.")
    parser.add_argument("--jd-text", default="", help="Raw job description text.")
    parser.add_argument("--jd-file", default="", help="Optional path to a file containing the job description.")
    parser.add_argument(
        "--compare-jd-files",
        nargs="+",
        default=[],
        help="Optional list of JD files for comparison mode.",
    )
    parser.add_argument("--eval-cases-file", default="", help="Optional JSON file with evaluation cases.")
    parser.add_argument("--materials-dir", default="sample_materials", help="Directory with resume material files.")
    parser.add_argument("--output-dir", default="outputs", help="Directory for generated Markdown reports.")
    parser.add_argument("--run-id", default="cli-run", help="Output report name without extension.")
    parser.add_argument("--openai-api-key", default="", help="Optional OpenAI-compatible API key.")
    parser.add_argument("--openai-base-url", default="", help="Optional OpenAI-compatible base URL.")
    parser.add_argument("--openai-model", default="", help="Optional model name for LLM enhancement.")
    return parser


def _load_jd_text(args: argparse.Namespace) -> str:
    if args.jd_text:
        return args.jd_text
    if args.jd_file:
        return Path(args.jd_file).read_text(encoding="utf-8")
    raise ValueError("Either --jd-text or --jd-file must be provided.")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    env_config = AppConfig.from_env()
    config = AppConfig(
        openai_api_key=args.openai_api_key or env_config.openai_api_key,
        openai_base_url=args.openai_base_url or env_config.openai_base_url,
        openai_model=args.openai_model or env_config.openai_model,
    )
    if args.eval_cases_file:
        result = evaluate_cases_file(
            cases_file=Path(args.eval_cases_file),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            config=config,
        )
        print(result.report_path)
        return 0

    if args.compare_jd_files:
        jd_inputs = [
            (Path(path).stem, Path(path).read_text(encoding="utf-8")) for path in args.compare_jd_files
        ]
        result = run_resume_tailor_compare(
            jd_inputs=jd_inputs,
            materials_dir=Path(args.materials_dir),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            config=config,
        )
        print(result.export_path)
        return 0

    jd_text = _load_jd_text(args)
    result = run_resume_tailor(
        jd_text=jd_text,
        materials_dir=Path(args.materials_dir),
        output_dir=Path(args.output_dir),
        run_id=args.run_id,
        config=config,
    )
    print(result.export_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
