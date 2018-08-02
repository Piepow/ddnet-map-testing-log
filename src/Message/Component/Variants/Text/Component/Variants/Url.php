<?php

namespace DDNet\MapTestingLog\Message\Component\Variants\Text\Component\Variants;

use DDNet\MapTestingLog\Message\Component;
use DDNet\MapTestingLog\User;

class Url extends Component
{
    public $url;

    public function __construct(array $source)
    {
        $this->url = $source['url'];
    }

    public static function isCorrectVariant($source): bool
    {
        return isset($source['url']);
    }
}
