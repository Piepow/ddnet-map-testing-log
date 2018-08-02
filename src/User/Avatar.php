<?php

namespace DDNet\MapTestingLog\User;

class Avatar
{
    public $url;
    public $size;

    public function __construct(string $url)
    {
        $this->url = $url;
        $this->size = 40;
    }
}
