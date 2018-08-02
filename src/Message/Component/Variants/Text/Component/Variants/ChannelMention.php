<?php

namespace DDNet\MapTestingLog\Message\Component\Variants\Text\Component\Variants;

use DDNet\MapTestingLog\Message\Component;
use DDNet\MapTestingLog\Channel;

class ChannelMention extends Component
{
    public $channel;

    public function __construct(array $source)
    {
        $this->channel = new Channel($source['channel-mention']);
    }

    public static function isCorrectVariant($source): bool
    {
        return isset($source['channel-mention']);
    }
}
