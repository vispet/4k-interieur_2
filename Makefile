###
# Builds this apps source
###

SHELL = /bin/bash

NODE_MODULES ?= node_modules
NPM_BIN = $(shell npm bin)
DEBUG = 0
ASSETS_BUILD_DIR ?= .build
BUILD_CACHE_DIR ?= .build-cache
SOURCE_DIR ?= static
PROJECT_DIR ?= project
IMAGEMIN_OPIMISATION_LEVEL = 7
SASS_STYLE ?= compressed
SASS_SOURCEMAP ?= none

# Default
all: build

# Release build
build: clean files fonts images favicons stylesheets javascripts python

# Development build
set_dev:
	@echo -e "\nActivating development modus\n"
	$(eval DEBUG = 1)
	$(eval IMAGEMIN_OPIMISATION_LEVEL = 0)
	$(eval SASS_STYLE = nested)
	$(eval SASS_SOURCEMAP = file)

build.dev: set_dev build

# Development start
start: build.dev
	@echo -e "\nStarting all processes in parallell!\n"
	@$(NPM_BIN)/shell-exec "make proc" \
						   "make watch" \
	 && echo -e "\n...GOODBYE...\n"

# Clean the build dir
clean:
	@echo -e "\nCleaning build target\n"
	@rm -rf $(ASSETS_BUILD_DIR)
	@rm -rf $(BUILD_CACHE_DIR)

# Copy files
files:
	@echo -e "\nCopy files\n"
	@if [[ -d "$(SOURCE_DIR)/files" ]]; then \
		mkdir -p $(ASSETS_BUILD_DIR)/files; \
		cp -rf $(SOURCE_DIR)/files/* $(ASSETS_BUILD_DIR)/files/; \
	fi

# Copy fonts
fonts: fonts.msg fonts.bootstrap fonts.files

fonts.msg:
	@echo -e "\nCopy fonts\n"

fonts.bootstrap:
	@mkdir -p $(ASSETS_BUILD_DIR)/fonts;
	@cp -r $(NODE_MODULES)/bootstrap-sass/assets/fonts/bootstrap/ \
		$(ASSETS_BUILD_DIR)/fonts/bootstrap/

fonts.files:
	@if [[ -d "$(SOURCE_DIR)/fonts" ]]; then \
		cp -rf $(SOURCE_DIR)/fonts/* $(ASSETS_BUILD_DIR)/fonts/; \
	fi

# Image processing
images: images.images images.fontello images.grunticons

images.images: images.images.bitmap images.images.svg

images.images.bitmap:
	@echo -e "\nProcessing bitmap images\n"
	@build-tools/bitmap-min.js $(SOURCE_DIR)/img/bitmap \
							   $(ASSETS_BUILD_DIR)/img/bitmap \
							   $(IMAGEMIN_OPIMISATION_LEVEL)

images.images.svg:
	@echo -e "\nProcessing vector images\n"
	@build-tools/vector-min.js $(SOURCE_DIR)/img/svg \
						       $(ASSETS_BUILD_DIR)/img/svg

images.fontello:
	@echo -e "\nProcessing font icons\n"
	@if [[ -f "$(SOURCE_DIR)/fontello/config.json" ]]; then \
		mkdir -p $(BUILD_CACHE_DIR)/fontello-css/; \
		mkdir -p $(ASSETS_BUILD_DIR)/fonts/fontello/; \
		$(NPM_BIN)/fontello-cli install \
			--css $(BUILD_CACHE_DIR)/fontello-css/ \
			--font $(ASSETS_BUILD_DIR)/fonts/fontello/ \
			--config $(SOURCE_DIR)/fontello/config.json; \
		mkdir -p $(BUILD_CACHE_DIR)/scss/fontello/; \
		for file in $(BUILD_CACHE_DIR)/fontello-css/*.css; do \
			mv $$file $(BUILD_CACHE_DIR)/scss/fontello/_$$(basename $$file .css).scss; \
		done; \
	fi

images.grunticons:
	@echo -e "\nProcessing data uri vectors\n"
	@if [[ -d "$(SOURCE_DIR)/img/icons/" ]]; then \
		build-tools/grunticon-cli.js $(SOURCE_DIR)/img/icons/**/*.svg $(ASSETS_BUILD_DIR)/img/icons/; \
	fi

# Favicons
favicons:
	@echo -e "\nGenerate favicons\n"
	@if [[ -f "$(SOURCE_DIR)/img/favicons/favicon.png" ]]; then \
        mkdir -p $(PROJECT_DIR)/templates/generated/; \
		build-tools/favicon-cli.js $(SOURCE_DIR)/img/favicons/favicon.png \
									$(ASSETS_BUILD_DIR)/img/favicons/ \
									$(PROJECT_DIR)/templates/generated/favicons.html; \
	fi

# stylesheets
stylesheets:
	@echo -e "\nCompiling stylesheets\n"
	@echo -e "\$$assets-build-dir: \"$$PWD/$(ASSETS_BUILD_DIR)\";" > \
		build-tools/generated-assets-build-dir.scss
	@mkdir -p $(ASSETS_BUILD_DIR)/css/
	@mkdir -p $(BUILD_CACHE_DIR)/scss/
	@cp $(NODE_MODULES)/slick-lightbox/dist/slick-lightbox.css $(BUILD_CACHE_DIR)/scss/_slick-lightbox.scss
	@sass --compass --scss \
		  --style $(SASS_STYLE) \
		  --sourcemap=$(SASS_SOURCEMAP) \
		  --load-path $(BUILD_CACHE_DIR)/scss \
		  --load-path $(NODE_MODULES)/bootstrap-sass/assets/stylesheets \
		  --load-path $(NODE_MODULES) \
		  $(SOURCE_DIR)/scss/style.scss $(ASSETS_BUILD_DIR)/css/style.css

# javascripts
javascripts: javascripts.jshint javascripts.copy javascripts.browserify

javascripts.jshint:
	@echo -e "\nRun jshint\n"
	@$(NPM_BIN)/jshint --reporter $(NODE_MODULES)/jshint-stylish-ex/stylish.js $(SOURCE_DIR)/js/

javascripts.copy:
	@echo -e "\nCopy dependencies\n"
	@mkdir -p $(ASSETS_BUILD_DIR)/js/
	@cp $(NODE_MODULES)/html5shiv/dist/html5shiv.min.js $(ASSETS_BUILD_DIR)/js/html5shiv.min.js
	@cp $(NODE_MODULES)/respond.js/dest/respond.min.js $(ASSETS_BUILD_DIR)/js/respond.min.js

javascripts.browserify:
	@echo -e "\nCompiling javascripts\n"
	@if [[ $(DEBUG) == 1 ]]; then \
		$(NPM_BIN)/browserify -d $(SOURCE_DIR)/js/main.js | \
			$(NPM_BIN)/exorcist $(ASSETS_BUILD_DIR)/js/main.js.map > $(ASSETS_BUILD_DIR)/js/main.js; \
	else \
		$(NPM_BIN)/browserify -g uglifyify $(SOURCE_DIR)/js/main.js | \
			$(NPM_BIN)/uglifyjs -c > $(ASSETS_BUILD_DIR)/js/main.js; \
	fi

# lint python and run tests
python: python.pep8 python.pylint python.django.tests python.django.locales

python.pep8:
	@echo -e "\nPep8 python style check\n"
	@pep8 --exclude=migrations $(PROJECT_DIR)

python.pylint:
	@echo -e "\nPylint code quality test\n"
	@pylint $$(ls $(PROJECT_DIR) | grep -v "templates\|locales" | awk '{ ORS=" " } { print "$(PROJECT_DIR)/"$$0}') -r n -f colorized --rcfile pylintrc

python.django.tests:
	@echo -e "\nRunning django tests\n"
	@$(PROJECT_DIR)/manage.py test --noinput

python.django.locales:
	@if [[ -d "$(PROJECT_DIR)/locales" ]]; then \
		echo -e "Compiling interface translations\n"; \
		$(PROJECT_DIR)/manage.py compilemessages; \
	fi

# Process watcher
watch:
	@echo -e "Watching sources"
	@$(NPM_BIN)/shell-exec "make watch.assets.files" \
						   "make watch.assets.fonts" \
						   "make watch.assets.images.bitmap" \
						   "make watch.assets.images.svg" \
						   "make watch.assets.images.fontello" \
						   "make watch.assets.images.grunticons" \
						   "make watch.assets.stylesheets" \
						   "make watch.assets.javascripts.jshint" \
						   "make watch.assets.javascripts.watchify" \
						   "make watch.server.locales" \
						   "make watch.server.checks"

watch.assets.files:
	@if [[ -d "$(SOURCE_DIR)/files/" ]]; then \
		$(NPM_BIN)/chokidar "$(SOURCE_DIR)/files/**/*" -c "make set_dev files" -d 1000; \
	fi

watch.assets.fonts:
	@if [[ -d "$(SOURCE_DIR)/fonts/" ]]; then \
		$(NPM_BIN)/chokidar "$(SOURCE_DIR)/fonts/**/*" -c "make set_dev fonts.files" -d 1000; \
	fi

watch.assets.images.bitmap:
	@$(NPM_BIN)/chokidar "$(SOURCE_DIR)/img/bitmap/**/*.{png,jpg,gif}" -c "make set_dev images.images.bitmap" -d 3000

watch.assets.images.svg:
	@$(NPM_BIN)/chokidar "$(SOURCE_DIR)/img/svg/**/*.svg" -c "make set_dev images.images.svg" -d 3000

watch.assets.images.fontello:
	@$(NPM_BIN)/chokidar "$(SOURCE_DIR)/fontello/config.json" -c "make set_dev images.fontello stylesheets" -d 3000

watch.assets.images.grunticons:
	@$(NPM_BIN)/chokidar "$(SOURCE_DIR)/img/icons/**/*.svg" -c "make set_dev images.grunticons" -d 2000

watch.assets.stylesheets: set_dev
	@echo -e "\$$assets-build-dir: \"$(ASSETS_BUILD_DIR)\";" > \
		build-tools/generated-assets-build-dir.scss;
	@mkdir -p $(ASSETS_BUILD_DIR)/css/
	@sass --compass --scss \
		  --sourcemap=$(SASS_SOURCEMAP) \
		  --style $(SASS_STYLE) \
		  --load-path $(BUILD_CACHE_DIR)/scss \
		  --load-path $(NODE_MODULES)/bootstrap-sass/assets/stylesheets \
		  --load-path $(NODE_MODULES) \
		  --watch $(SOURCE_DIR)/scss/:./$(ASSETS_BUILD_DIR)/css/

watch.assets.javascripts.jshint:
	@$(NPM_BIN)/chokidar "$(SOURCE_DIR)/js/**/*.js" -c "make set_dev javascripts.jshint" -d 2000

watch.assets.javascripts.watchify: set_dev
	@$(NPM_BIN)/watchify -v -d $(SOURCE_DIR)/js/main.js -o "$(NPM_BIN)/exorcist $(ASSETS_BUILD_DIR)/js/main.js.map > $(ASSETS_BUILD_DIR)/js/main.js"

watch.server.locales:
	@$(NPM_BIN)/chokidar "$(PROJECT_DIR)/locales/**/*.po" -c "make set_dev python.django.locales" -d 10000

watch.server.checks:
	@$(NPM_BIN)/chokidar "$(PROJECT_DIR)/**/*.py" -c "make set_dev python.pep8 python.pylint python.django.tests" -d 10000

proc:
	@echo -e "Run servers"
	@$(NPM_BIN)/shell-exec "make proc.web" "make proc.worker"

proc.web:
	@$(PROJECT_DIR)/manage.py runserver

proc.worker:
	@$(NPM_BIN)/watchy -k -w "$(PROJECT_DIR)/**/*.py" -- celery -A project worker --workdir $(PROJECT_DIR)/
