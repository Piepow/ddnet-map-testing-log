<?php

namespace DDNet\MapTestingLog;

use DirectoryIterator;
use DDNet\MapTestingLog\MapTestingLog;

class Fetcher
{
    private $logPath;

    public function __construct(string $logPath)
    {
        $this->logPath = $logPath;
    }

    public function byName(string $name): MapTestingLog
    {
        $directoryIterator = new DirectoryIterator($this->logPath);
        foreach ($directoryIterator as $fileinfo) {
            if (!$fileinfo->isDot()) {
                if ($name == $fileinfo->getBasename('.html')) {
                    return new MapTestingLog($fileinfo->getPathname());
                }
            }
        }
    }

    public function all(): array
    {
        $list = [];
        $directoryIterator = new DirectoryIterator($this->logPath);
        foreach ($directoryIterator as $fileinfo) {
            if (!$fileinfo->isDot()) {
                $list[] = new MapTestingLog($fileinfo->getPathname());
            }
        }
        return $list;
    }
}
