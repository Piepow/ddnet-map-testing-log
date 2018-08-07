<?php

$projectConfig = include 'common/project.php';
$projectPath = $projectConfig['path'];

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
