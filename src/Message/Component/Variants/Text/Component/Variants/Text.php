<?php

namespace DDNet\MapTestingLog\Message\Component\Variants\Text\Component\Variants;

use DDNet\MapTestingLog\Message\Component;
use DDNet\MapTestingLog\User;

class Text extends Component
{
    public $text;

    public function __construct(array $source)
    {
        $this->text = $source['text'];
    }

    public static function isCorrectVariant($source): bool
    {
        return isset($source['text']);
    }
}
