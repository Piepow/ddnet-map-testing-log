<?php

namespace DDNet\MapTestingLog;

use DDNet\MapTestingLog\User\Avatar;

class User
{
    public $name;
    public $discriminator;
    public $avatar;
    public $roles;

    public function __construct(array $source)
    {
        $this->name = $source['name'];
        $this->discriminator = (int)$source['discriminator'];
        $this->avatar = new Avatar($source['avatar']);
        $this->roles = $source['roles'];
    }

    public function getProminentRole()
    {
        if (empty($this->roles)) {
            return 'generic';
        }

        return array_values($this->roles)[0];
    }
}
