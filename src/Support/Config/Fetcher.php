<?php

namespace DDNet\MapTestingLog\Support\Config;

use DirectoryIterator;

class Fetcher
{
    private $configPath;

    public function __construct(string $configPath)
    {
        $this->configPath = $configPath;
    }

    public function all(): array
    {
        $config = [];
        $directoryIterator = new DirectoryIterator($this->configPath);
        foreach ($directoryIterator as $fileinfo) {
            if (!$fileinfo->isDot()) {
                $config[$fileinfo->getBasename('.php')] = include(
                    $fileinfo->getPathname()
                );
            }
        }
        return $config;
    }
}
