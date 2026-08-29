.PHONY: package release

package:
	@python3 scripts/release.py

release:
	@python3 scripts/release.py "$(VERSION)"
