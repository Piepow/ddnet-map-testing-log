<?php

namespace DDNet\MapTestingLog\Message\Component\Variants;

use DDNet\MapTestingLog\Message\Component\Variants\Text\Component\Variants as
    ComponentVariants;
use DDNet\MapTestingLog\Message\Component;

class Text extends Component
{
    public $components;

    public function __construct(array $source)
    {
        $this->instanciateComponents(
            $source['text']
        );
    }

    private function instanciateComponents(array $sourceComponents)
    {
        $this->components = Component::instanciateMany(
            $sourceComponents,
            [
                ComponentVariants\Text::class,
                ComponentVariants\UserMention::class,
                ComponentVariants\ChannelMention::class,
                ComponentVariants\CustomEmoji::class
            ]
        );
    }

    public static function isCorrectVariant($source): bool
    {
        return isset($source['text']);
    }

    public static function hasComponents(): bool
    {
        return true;
    }
}
