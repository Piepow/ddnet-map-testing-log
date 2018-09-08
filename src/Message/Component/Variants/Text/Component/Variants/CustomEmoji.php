<?php

namespace DDNet\MapTestingLog\Message\Component\Variants\Text\Component\Variants;

use DDNet\MapTestingLog\Message\Component;

class CustomEmoji extends Component
{
    public $name;
    public $id;

    public function __construct(array $source)
    {
        $source = $source['custom-emoji'];
        $this->name = $source['name'];
        $this->id = $source['id'];
    }

    public static function isCorrectVariant($source): bool
    {
        return isset($source['custom-emoji']);
    }
}
