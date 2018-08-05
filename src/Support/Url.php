<?php

namespace DDNet\MapTestingLog\Support;

class Url
{
    public static function getHttpResponseCode(
        string $url,
        bool $followRedirects = true
    ): bool {
        $headers = @get_headers($url);
        if ($headers && is_array($headers)) {
            if ($followRedirects) {
                // want last error code, so start from the end
                $headers = array_reverse($headers);
            }

            foreach ($headers as $header) {
                if (preg_match(
                    '/^HTTP\/\S+\s+([1-9][0-9][0-9])\s+.*/',
                    $header,
                    $matches
                )) {
                    $responseCode = $matches[1];
                    return $responseCode;
                }
            }

            // no HTTP/xxx found in headers
            return false;
        }

        // no headers
        return false;
    }
}
