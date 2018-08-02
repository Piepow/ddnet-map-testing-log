<?php

namespace DDNet\MapTestingLog\Message\Component\Variants\Text\Component\Variants;

use DDNet\MapTestingLog\Message\Component;
use DDNet\MapTestingLog\User;

class UserMention extends Component
{
    public $user;

    public function __construct(array $source)
    {
        $this->user = new User($source['user-mention']);
    }

    public static function isCorrectVariant($source): bool
    {
        return isset($source['user-mention']);
    }
}
