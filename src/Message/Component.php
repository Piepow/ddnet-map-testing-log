<?php

namespace DDNet\MapTestingLog\Message;

abstract class Component
{
    abstract public static function isCorrectVariant($component): bool;

    public static function hasComponents(): bool
    {
        return false;
    }

    public static function instanciateMany(
        array $sourceComponents,
        array $componentVariants
    ): array {
        $components = [];
        foreach ($sourceComponents as $sourceComponent) {
            foreach ($componentVariants as $componentVariant) {
                if ($componentVariant::isCorrectVariant($sourceComponent)) {
                    $components[] = new $componentVariant($sourceComponent);
                    break;
                }
            }
        }
        return $components;
    }
}
