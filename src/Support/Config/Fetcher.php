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

    public function fetchAll(): array
    {
        $config = [];
        $directoryIterator = new DirectoryIterator($this->configPath);
        foreach ($directoryIterator as $fileinfo) {
            if ($fileinfo->isFile()) {
                $basename = $fileinfo->getBaseName('.php');
                $config[$basename] = $this->fetchFile($basename);
            }
        }
        return $config;
    }

    public function fetchFile(string $basename)
    {
        return include $this->configPath . $basename . '.php';
    }
}
