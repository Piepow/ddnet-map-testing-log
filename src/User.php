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
        $this->processAndSetRoles($source['roles']);
    }

    private function processAndSetRoles(array $roles)
    {
        foreach ($roles as $role) {
            $role = strtolower($role);
            $role = str_replace(' ', '-', $role);
            $this->roles[] = $role;
        }
    }

    public function getProminentRole()
    {
        if (empty($this->roles)) {
            return 'generic';
        }

        return array_values($this->roles)[0];
    }
}
