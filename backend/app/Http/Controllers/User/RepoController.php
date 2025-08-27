<?php

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use App\Services\User\RepoService;

class RepoController extends Controller{

    public function fetchTree(Request $request){
        
        $url = $request->input('url');

        if(!$url){
            return $this->responseJSON(null, 'Reposiory URL is required', 400);
        }

        $tree = RepoService::fetchTree($url);

        if(!$tree){
            return $this->responseJSON(null, 'Failed to fetch repo tree', 500);
        }

        return $this->responseJSON($tree);
    }
    
}
