<?php

namespace App\Services\User;

class RepoService{
    
    public static function fetchTree($url){


    }

    public function parseRepoURL($url){
        
        $parts = parse_url($url);
        $data = explode('/', trim($parts['path'], '/'));
        
        $parsed = [
            'owner' => $data[0] ?? null,
            'repo' => $data[1] ?? null
        ];

        return $parsed;
    }
}
