<?php

namespace DDNet\MapTestingLog;

class Channel
{
    public $name;

    public function __construct(array $source)
    {
        $this->name = $source['name'];
    }
}
