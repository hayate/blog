<!doctype html>
<html class="no-js" lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{get('title', 'Blog')}}</title>
    <link rel="stylesheet" href="/assets/foundation/css/foundation.css" />
    <script src="/assets/foundation/js/vendor/modernizr.js"></script>
  </head>
  <body>

    <div class="row">
      <div class="small-12 columns">
        <h3 class="subheader">Login</h3>
      </div>
    </div>

    <div class="row">
      <div class="small-12 columns">
        <form method="post" action="/login/submit">
          <div class="row">
            <div class="small-8 small-centered columns">
              <div class="row">
                <div class="small-2 columns">
                  <label for="username" class="right inline">Username</label>
                </div>
                <div class="small-5 columns">
                  <input type="text" id="username" name="username" placeholder="username" />
                </div>
                <div class="small-5 columns">&nbsp;</div>
              </div>
            </div>
          </div>

          <div class="row">
            <div class="small-8 small-centered columns">
              <div class="row">
                <div class="small-2 columns">
                  <label for="password" class="right inline">Password</label>
                </div>
                <div class="small-5 columns">
                  <input type="text" id="password" name="password" placeholder="password" />
                </div>
                <div class="small-5 columns">&nbsp;</div>
              </div>
            </div>
          </div>

          <div class="row">
            <div class="small-8 small-centered columns">
              <div class="row">
                <div class="small-5 small-offset-5 columns">
                  <input type="submit" aria-label="submit form" value="Submit" class="button small" />
                </div>
              </div>
            </div>
          </div>

        </form>
      </div>
    </div>

    <script src="/assets/foundation/js/vendor/jquery.js"></script>
    <script src="/assets/foundation/js/foundation.min.js"></script>
    <script>
      $(document).foundation();
    </script>
  </body>
</html>
