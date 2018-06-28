<?php

namespace DDNet\MapTestingLog;

class MapTestingLog
{
    private $file;

    public function __construct(string $file)
    {
        $this->file = $file;
    }

    public function getName(): string
    {
        return basename($this->file, '.html');
    }

    public function getHtml(): string
    {
        return file_get_contents($this->file);
    }
}
