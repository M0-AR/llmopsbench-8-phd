.PHONY: test bench clean
test:
	pytest -q
bench:
	python experiments/run_all.py --out results/summary.json
clean:
	rm -f results/summary.json results/*.json
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null; true
