<?php

namespace DDNet\MapTestingLog\User;

use DDNet\MapTestingLog\Support\Url;
use DDNet\MapTestingLog\Support\Container\Access as ContainerAccess;

class Avatar
{
    const SIZE = 40;

    public $id;

    public function __construct(array $source)
    {
        $this->id = $source['id'];
    }
}
