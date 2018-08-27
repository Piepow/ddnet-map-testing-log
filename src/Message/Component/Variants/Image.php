<?php

namespace DDNet\MapTestingLog\Message\Component\Variants;

use DDNet\MapTestingLog\Message\Component;

class Image extends Component
{
    public $id;
    public $basename;
    public $extension;

    public function __construct(array $source)
    {
        $source = $source['image'];
        $this->id = $source['id'];
        $this->basename = $source['basename'];
        $this->extension = $source['extension'];
    }

    public static function isCorrectVariant($source): bool
    {
        return isset($source['image']);
    }
}
