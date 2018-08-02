<?php

namespace DDNet\MapTestingLog\Message\Component\Variants;

use DDNet\MapTestingLog\Message\Component;

class Image extends Component
{
    public $url;
    public $basename;
    public $extension;

    public function __construct(array $source)
    {
        $source = $source['image'];
        $this->url = $source['url'];
        $this->basename = $source['basename'];
        $this->extension = $source['extension'];
    }

    public static function isCorrectVariant($source): bool
    {
        return isset($source['image']);
    }
}
