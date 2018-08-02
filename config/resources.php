<?php

$projectPath = '/home/plushie/Documents/web/ddnet-map-testing-log/';

return [
    'views' => [
        'path' => $projectPath . 'resources/views/',
        'componentRenderer' => [
            'subPath' => 'partials/message/',
            'stepSubPath' => 'component/variants/'
        ]
    ],
    'mapTestingLogs' => [
        'path' => $projectPath . 'resources/logs/'
    ],
];
