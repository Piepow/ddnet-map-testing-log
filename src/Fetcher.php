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
                if ($name == $fileinfo->getBasename('.json')) {
                    return new MapTestingLog(
                        json_decode(
                            file_get_contents($fileinfo->getPathname()),
                            true
                        )
                    );
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
                if ($fileinfo->getExtension() == 'json') {
                    $list[] = MapTestingLog::getAsChannel(
                        json_decode(
                            file_get_contents($fileinfo->getPathname()),
                            true
                        )
                    );
                }
            }
        }
        return $list;
    }
}
