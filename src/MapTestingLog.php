<?php

namespace DDNet\MapTestingLog;

use DDNet\MapTestingLog\Message;
use DDNet\MapTestingLog\Channel;

class MapTestingLog
{
    public $name;
    public $topic;
    public $messages;

    public function __construct(array $source)
    {
        $this->name = $source['name'];
        $this->topic = $source['topic'];
        $this->messages = [];
        foreach ($source['messages'] as $message) {
            $this->messages[] = new Message($message);
        }
    }

    public static function getAsChannel(array $source): Channel
    {
        return new Channel($source);
    }
}
