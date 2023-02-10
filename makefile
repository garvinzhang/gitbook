.PHONY: commit

commit:
	git status;
	git add --all;
	git commit -m "update"

