<?php

require(dirname(__DIR__) . '/vendor/autoload.php');

use Slim\App;
use Slim\Views;
use Psr\Http\Message\ServerRequestInterface as Request;
use Psr\Http\Message\ResponseInterface as Response;
use DDNet\MapTestingLog\Support\Config;
use DDNet\MapTestingLog\Support\Asset;
use DDNet\MapTestingLog;

// =============================
// Slim framework initialization
// =============================

$config = [
    'settings' => [
        'displayErrorDetails' => true
    ],
];

$app = new App($config);

$container = $app->getContainer();

$container['config'] = (new Config\Fetcher(
    dirname(__DIR__) . '/config/'
))->all();

$container['view'] = function ($container) {
    return new Views\PhpRenderer(
        dirname(__DIR__) . '/resources/templates/'
    );
};

$container['mapTestingLogFetcher'] = function ($container) {
    return new MapTestingLog\Fetcher(dirname(__DIR__) . '/resources/logs/');
};

$container['assetFetcher'] = function ($container) {
    return new Asset\Fetcher($container['config']['app']['url']);
};

// =======
// Routing
// =======

$app->get('/show/{name}', function (
    Request $request,
    Response $response,
    $args
) {
    $name = $args['name'];
    $log = $this->mapTestingLogFetcher->byName($name);
    $logList = $this->mapTestingLogFetcher->all();
    $this->view->render($response, 'show.phtml', [
        'log' => $log,
        'logList' => $logList,
        'router' => $this->router,
        'assetFetcher' => $this->assetFetcher
    ]);
    return $response;
})->setName('show.name');

$app->run();
