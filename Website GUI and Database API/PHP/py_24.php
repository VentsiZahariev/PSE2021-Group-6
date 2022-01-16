<!DOCTYPE html>
<html class="has-navbar-fixed-top">
  <head>
   <meta http-equiv="refresh" content="180">
    <meta http-equiv="content-type" content="text/html:charset=utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PSE Group 6 Data</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
    <link rel="stylesheet" href="custom.css">
    <script src="https://kit.fontawesome.com/ab531e491f.js" crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script src="index.js"></script>
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
  </head>
  <body>
    <!-- navbar -->
    <nav class="navbar is-primary is-fixed-top">
      <div class="navbar-brand">

          <div class="navbar-item">
              <span class="icon is-size-5">
                  <i class="fas fa-cloud-sun"></i>
              </span>
          </div>

          <div class="navbar-item">
              <h1 class="is-size-4 has-text-weight-bold">
                  Gorilla Weather
              </h1>
          </div>

          <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarResise">
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
          </a>

      </div>

      <div class="navbar-menu" id="navbarResise">
          <div class="navbar-start has-text-weight-bold">
              <a href="index.php" class="navbar-item">
                Graphs
              </a>

              <a href="py-saxion-home.html" class="navbar-item">
                  Sensors
              </a>
          </div>

          <div class="navbar-end">
              <div class="navbar-item">
                  <div class="field is-grouped">
                      <p class="control">
                          <a href="about.html" class="button has-text-weight-bold is-light is-rounded">
                              <span class="icon">
                                  <i class="far fa-address-card" aria-hidden="true"></i>
                              </span>
                              <span>
                                  About
                              </span>
                          </a>
                      </p>
                      <p class="control">
                          <a href="https://github.com/VentsiZahariev/PSE2021-Group-6" class="button is-info is-rounded">
                                 <span class="icon">
                                  <i class="fab fa-github" aria-hidden="true"></i>
                              </span>
                              <span>
                                  Github
                              </span>
                          </a>
                      </p>
                  </div>
              </div>
          </div>
      </div>
 </nav>

  <!-- dropdowns -->
  <section class="section pb-6">
    <div class="container">

      <div class="columns is-vcentered">

        <div class="column is-3">
           <div class="dropdown is-fullwidth">
            <div class="dropdown-trigger">
              <button class="button is-fullwidth" aria-haspopup="true" aria-controls="dropdown-menu3">
                <span>Date</span>
                <span class="icon is-small">
                  <i class="fas fa-angle-down" aria-hidden="true"></i>
                </span>
              </button>
            </div>
            <div class="dropdown-menu" id="dropdown-menu3" role="menu">
              <div class="dropdown-content">
                <div class="container dropdown-item">
                  <a href="index.php" input type="button" class="button is-fullwidth">Last 6hours</a>
                </div>
                <div class="container dropdown-item">
                  <a href="py_six.php" input type="button" class="button is-fullwidth">Last 12hours</a>
                </div>
                  <div class="container dropdown-item">
                  <a input type="button" class="button is-link is-fullwidth">Last 24hours</a>
                </div>
                <div class="container dropdown-item">
                  <a href="py_2days.php" input type="button" class="button is-fullwidth">Last 2days</a>
                </div>
                <div class="container dropdown-item">
                  <a href="py_4days.php" input type="button" class="button is-fullwidth">Last 4days</a>
                </div>
                <div class="container dropdown-item">
                  <a href="py_6days.php" input type="button" class="button is-fullwidth">Last 6days</a>
                </div>
                <div class="container dropdown-item">
                  <a href="py_7days.php" input type="button" class="button is-fullwidth">Last Week</a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-6 has-text-centered">
          <div class="control">
            <lable class="radio mx-2">
              <input type="radio" id="showAll" name="selectLine" checked>
              Show all
            </lable>
            <lable class="radio mx-2">
              <input type="radio" id="hideEns" name="selectLine">
              Enschede
            </lable>
            <lable class="radio mx-2">
              <input type="radio" id="hideWie1" name="selectLine">
              Wierden - In
            </lable>
            <lable class="radio mx-2">
              <input type="radio" id="hideGro" name="selectLine">
              Gronau
            </lable>
            <lable class="radio mx-2">
              <input type="radio" id="hideWie2" name="selectLine">
              Wierden - Out
            </lable>
          </div>
        </div>

        <div class="column">
          <hr class="is-rounded">
        </div>

      </div>

    </div>
  </section>
  <!-- graphs -->
  <section class="section pt-0">
<?php
include("py_day.php")
?>
  </section>
  </body>

</html>

