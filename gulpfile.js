const gulp = require("gulp");

const css = () => {
    const postCSS = require("gulp-postcss");
    var sass = require("gulp-sass");
    const minify = require("gulp-csso");
    sass.compiler = require("node-sass");
    return gulp
        .src(__dirname + "/assets/scss/styles.scss")
        // tailwind css를 css로 바꿔주는 라인
        .pipe(sass().on("error", sass.logError))
        .pipe(postCSS([require("tailwindcss"), require("autoprefixer")]))
        .pipe(minify())
        // 바꾼 결과를 /static/css 폴더에 저장
        .pipe(gulp.dest("./static/css"));
};
exports.default = css;